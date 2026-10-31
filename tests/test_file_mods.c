/* Exercise direct file mappings, original fallback, directory merging and writable saves. */
#include "../src/runtime_file.c"
#include <assert.h>
static int32_t guest_errno;
int32_t *runtime_errno(void) { return &guest_errno; }
int32_t runtime_guest_errno(int e) { return e; }
uintptr_t runtime_lookup(const RuntimeExport *table,size_t n,const char *name) {
    for (size_t i=0;i<n;++i) if (!strcmp(table[i].name,name)) return (uintptr_t)table[i].function;
    return 0;
}
int main(void) {
    char root[]="./bbport-mod-files-XXXXXX";
    assert(mkdtemp(root));
    char game[512],user[512],source[512],link[512];
    snprintf(game,sizeof(game),"%s/game",root);
    snprintf(user,sizeof(user),"%s/user",root);
    snprintf(source,sizeof(source),"%s/mod.dcx",root);
    snprintf(link,sizeof(link),"%s/game/asset.dcx",root);
    assert(!mkdir(game,0755));
    FILE *f=fopen(source,"w"); assert(f); assert(fputs("modded",f)>=0); assert(!fclose(f));
    f=fopen(link,"w"); assert(f); fputs("original",f); fclose(f);
    char manifest[512],added[512];
    snprintf(manifest,sizeof(manifest),"%s/mod-files.tsv",root);
    snprintf(added,sizeof(added),"%s/new",root); assert(!mkdir(added,0755));
    f=fopen(manifest,"wb"); assert(f);
    fprintf(f,"BBMODS1\r\nasset.dcx\t%s\r\nnew\t%s\r\nnew/added.dcx\t%s\r\n",source,added,source);
    assert(!fclose(f));
#ifdef _WIN32
    assert(!_putenv_s("BB_MOD_FILES",manifest));
#else
    assert(!setenv("BB_MOD_FILES",manifest,1));
#endif
    runtime_file_configure(game,user);
    for (int i=0;i<3;++i) {
        const char *path=i==0 ? "/app0/asset.dcx" : i==1 ? "/hostapp/asset.dcx" : "asset.dcx";
        int fd=(int)do_open(path,0,0); assert(fd>=3);
        char content[8]={0}; assert(do_read(fd,content,6)==6 && !strcmp(content,"modded"));
        GuestStat info; assert(!do_stat(path,&info) && info.size==6);
        assert(!do_close(fd));
        assert(do_open(path,2,0)==-EROFS);
        assert(do_open(path,0x400,0)==-EROFS);
        assert(do_truncate(path,0)==-EROFS);
        assert(path_op(path,2,0)==-EROFS);
        assert(do_rename(path,"/data/moved")==-EROFS);
    }
    int dir=(int)do_open("/app0",0x20000,0); assert(dir>=3);
    char entries[1024]; int64_t count=do_getdents(dir,entries,sizeof(entries),NULL); assert(count>0);
    int found=0;
    for (int64_t p=0;p<count;) {
        uint16_t length; memcpy(&length,entries+p+4,2);
        assert(length);
        if (!strcmp(entries+p+8,"asset.dcx")) { assert(entries[p+6]==8); found=1; }
        p+=length;
    }
    assert(found && !do_close(dir));
    int nested=(int)do_open("/hostapp/new/ADDED.dcx",0,0); assert(nested>=3);
    assert(!do_close(nested));
    dir=(int)do_open("/app0/new",0x20000,0); assert(dir>=3);
    Listing *listing=get(dir)->dir; found=0;
    for (size_t i=0;i<listing->count;++i) if (!strcmp(listing->names+listing->offsets[i],"added.dcx")) found++;
    assert(found==1 && !do_close(dir));
    char translated[1024]; assert(translate("/app0/../asset.dcx",translated,sizeof(translated))==EACCES);
    f=fopen(link,"r"); assert(f); char original[16]={0}; assert(fread(original,1,8,f)==8); fclose(f);
    assert(!strcmp(original,"original"));
    assert(!translate("/app0/untouched.dcx",translated,sizeof(translated)));
    char fallback[1024]; snprintf(fallback,sizeof(fallback),"%s/untouched.dcx",game);
    assert(!strcmp(translated,fallback));
    assert(!translate("/data/asset.dcx",translated,sizeof(translated)));
    snprintf(fallback,sizeof(fallback),"%s/data/asset.dcx",user); assert(!strcmp(translated,fallback));
    int save=(int)do_open("/data/test-save",0x202,0644); assert(save>=3);
    assert(do_write(save,"save",4)==4 && !do_close(save));
    assert(!path_op("/data/test-save",2,0));
    f=fopen(manifest,"wb"); assert(f); fputs("BBMODS1\n",f); fclose(f);
    runtime_file_configure(game,user);
    int clean=(int)do_open("/app0/asset.dcx",0,0); assert(clean>=3);
    memset(original,0,sizeof(original)); assert(do_read(clean,original,8)==8);
    assert(!strcmp(original,"original") && !do_close(clean));
    assert(!unlink(link) && !unlink(source) && !rmdir(game));
    const char *dirs[]={"temp0","download0","data"};
    for (int i=0;i<3;++i) { char p[1024]; snprintf(p,sizeof(p),"%s/%s",user,dirs[i]); assert(!rmdir(p)); }
    assert(!rmdir(user) && !unlink(manifest) && !rmdir(added) && !rmdir(root));
    puts("Guest mod files: reads, stat, merged listing, readonly assets and writable saves PASS");
}
