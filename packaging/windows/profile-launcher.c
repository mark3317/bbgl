/* Three test entry points share Bloodborne.exe but keep profiles and P2P ports separate.
 * Build with -DPLAYER_INDEX=1, 2 or 3 and place beside Bloodborne.exe. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shlobj.h>
#include <wchar.h>

#ifndef PLAYER_INDEX
#error PLAYER_INDEX must be defined
#endif
#if PLAYER_INDEX < 1 || PLAYER_INDEX > 3
#error PLAYER_INDEX must be 1, 2 or 3
#endif

static int fail(const wchar_t *message)
{
    MessageBoxW(NULL, message, L"Bloodborne test launcher", MB_OK | MB_ICONERROR);
    return 1;
}

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR arguments, int show)
{
    (void)instance; (void)previous; (void)show;
    static wchar_t root[32768], target[32768], profile[32768], command[32768];
    wchar_t local[MAX_PATH], port[16];
    DWORD length = GetModuleFileNameW(NULL, root, 32768);
    if (!length || length >= 32768)
        return fail(L"Could not resolve the launcher location.");
    wchar_t *slash = wcsrchr(root, L'\\');
    if (!slash)
        return fail(L"Could not resolve the installation folder.");
    *slash = L'\0';
    if (FAILED(SHGetFolderPathW(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, local)))
        return fail(L"Could not resolve LocalAppData.");
    if (swprintf(profile, 32768, L"%ls\\Bloodborne Game Launcher Player %d", local, PLAYER_INDEX) < 0 ||
        swprintf(target, 32768, L"%ls\\Bloodborne.exe", root) < 0 ||
        swprintf(command, 32768, L"\"%ls\" %ls", target, arguments ? arguments : L"") < 0)
        return fail(L"The launcher path or arguments are too long.");
    swprintf(port, 16, L"%d", 3657 + PLAYER_INDEX);
    if (!SetEnvironmentVariableW(L"BBGL_PROFILE_DIR", profile) ||
        !SetEnvironmentVariableW(L"BB_P2P_PORT", port) ||
        !SetEnvironmentVariableW(L"PYINSTALLER_RESET_ENVIRONMENT", L"1"))
        return fail(L"Could not configure the test profile.");
    const wchar_t *clear[] = {L"BB_CONFIG", L"BB_DATA_DIR", L"BB_USER_DIR", L"BBSC_DATA_DIR"};
    for (unsigned i = 0; i < sizeof(clear) / sizeof(clear[0]); ++i)
        SetEnvironmentVariableW(clear[i], NULL);
    STARTUPINFOW startup = {0};
    PROCESS_INFORMATION process = {0};
    startup.cb = sizeof(startup);
    if (!CreateProcessW(target, command, NULL, NULL, FALSE, 0, NULL, root, &startup, &process)) {
        wchar_t message[1024];
        swprintf(message, 1024, L"Could not start Bloodborne.exe (error %lu).\nKeep this file beside Bloodborne.exe.",
                 (unsigned long)GetLastError());
        return fail(message);
    }
    CloseHandle(process.hThread);
    WaitForSingleObject(process.hProcess, INFINITE);
    DWORD code = 1;
    GetExitCodeProcess(process.hProcess, &code);
    CloseHandle(process.hProcess);
    return (int)code;
}
