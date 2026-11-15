# sap-cred.ps1 - Windows Credential Manager helper for the SAP MCP launcher.
#
# The password is stored as a generic credential (DPAPI-protected by Windows),
# never in a JSON file. Dot-source this file; then use:
#   [SapCred]::ReadPassword($target, [ref]$user)   -> password or $null
#   [SapCred]::Write($target, $user, $password)     -> bool
#   [SapCred]::Delete($target)                      -> bool
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class SapCred
{
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct CREDENTIAL
    {
        public int Flags;
        public int Type;
        public string TargetName;
        public string Comment;
        public System.Runtime.InteropServices.ComTypes.FILETIME LastWritten;
        public int CredentialBlobSize;
        public IntPtr CredentialBlob;
        public int Persist;
        public int AttributeCount;
        public IntPtr Attributes;
        public string TargetAlias;
        public string UserName;
    }

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CredRead(string target, int type, int flags, out IntPtr credential);

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CredWrite(ref CREDENTIAL credential, int flags);

    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CredDelete(string target, int type, int flags);

    [DllImport("advapi32.dll")]
    public static extern void CredFree(IntPtr credential);

    public static string ReadPassword(string target, out string user)
    {
        user = null;
        IntPtr ptr;
        if (!CredRead(target, 1, 0, out ptr)) return null;
        try
        {
            CREDENTIAL c = (CREDENTIAL)Marshal.PtrToStructure(ptr, typeof(CREDENTIAL));
            user = c.UserName;
            return Marshal.PtrToStringUni(c.CredentialBlob, c.CredentialBlobSize / 2);
        }
        finally { CredFree(ptr); }
    }

    public static bool Write(string target, string user, string password)
    {
        CREDENTIAL c = new CREDENTIAL();
        c.Type = 1;
        c.TargetName = target;
        c.UserName = user;
        c.Persist = 2;
        byte[] bytes = Encoding.Unicode.GetBytes(password);
        c.CredentialBlobSize = bytes.Length;
        c.CredentialBlob = Marshal.AllocHGlobal(bytes.Length);
        try
        {
            Marshal.Copy(bytes, 0, c.CredentialBlob, bytes.Length);
            return CredWrite(ref c, 0);
        }
        finally { Marshal.FreeHGlobal(c.CredentialBlob); }
    }

    public static bool Delete(string target)
    {
        return CredDelete(target, 1, 0);
    }
}
'@
