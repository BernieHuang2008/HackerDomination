#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

// 生成所有可能的密码组合
vector<string> generatePasswords(int length, string charset)
{
    vector<string> passwords;
    if (length < 1)
    {
        return passwords;
    }
    if (length == 1)
    {
        for (char c : charset)
        {
            passwords.push_back(string(1, c));
        }
    }
    else
    {
        vector<string> subPasswords = generatePasswords(length - 1, charset);
        for (char c : charset)
        {
            for (string subPassword : subPasswords)
            {
                passwords.push_back(string(1, c) + subPassword);
            }
        }
    }
    return passwords;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        cout << "Usage: " << argv[0] << " <zipname>" << endl;
        return 1;
    }
    string filename = argv[1];     // 压缩包文件名
    string charset = "0123456789"; // 密码字符集
    int length = 4;                // 密码长度
    vector<string> passwords = generatePasswords(length, charset);

    for (string password : passwords)
    {
        printf("Trying: %s\n", password.c_str());
        string command = "unzip -o -P " + password + " " + filename + " > /dev/null 2>&1";
        int result = system(command.c_str());
        if (result == 0)
        {
            cout << "Password found: " << password << endl;
            return 0;
        }
    }
    cout << "Password not found." << endl;
    return 0;
}