#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void main_page();

int main()
{
    string input;

    cout << "Welcome to the Q MAIL Recover Center!" << endl;
    cout << "QMail is better then all, especially those who matched /.+@[gG]mail.com/" << endl;
    cout << endl;
    cout << "Please enter your username (e.g. admin@qmail.com): ";
    cin >> input;
    transform(input.begin(), input.end(), input.begin(), ::tolower);
    if (input == "great_peter_lee@qmail.com")
    {
        cout << "Welcome!" << endl;
        cout << "You've set 1 recovery question(s)." << endl;
        cout << "What is your sister's birthday?" << endl;
        cout << "Please answer: (in the format of 2024-01-01)" << endl;
        cin >> input;
        if (input == "1998-02-03")
        {
            cout << "Correct Answer!" << endl;
            cout << "Please enter your new password:" << endl;
            cin >> input;
            cout << "Password updated successfully, please keep it safe!" << endl;
            cout << "===================================================" << endl;
            main_page();
        }
        else
        {
            cout << "Wrong answer." << endl;
        }
    }
    else
    {
        cout << "Invalid username." << endl;
    }
}

void main_page()
{
    int input2;

    cout << "1. Starred     2. Starred     3. Starred" << endl;
    cout << "[ ]\b\b";
    cin >> input2;
    if (input2 >= 1 && input2 <= 3)
    {
        cout << "============================================" << endl;
        cout << "FROM    : great_peter_lee@qmail.com" << endl;
        cout << "TO      : great_peter_lee@qmail.com" << endl;
        cout << "Subject : A little note" << endl;
        cout << "Date    : 2024-01-01 00:00:00" << endl;
        cout << "============================================" << endl;
        cout << "Hello Peter," << endl;
        cout << "Here noted your passwords:" << endl;
        cout << "-----------------------------------------" << endl;
        cout << "|      Website     |      Password       |" << endl;
        cout << "| qmail.com        | plee666@qmail       |" << endl;
        cout << "| y.com            | plee666@y           |" << endl;
        cout << "| moz://b          | plee666@mozillb     |" << endl;
        cout << "| live.bighard.com | plee666@bighard     |" << endl;
        cout << "| unbreakable      | ***                 |" << endl;
        cout << "-----------------------------------------" << endl;
        cout << "Please keep it safe and NEVER FORGET!" << endl;
        cout << "                                      Yours," << endl;
        cout << "                                   Peter Lee" << endl;
        cout << "============================================" << endl;
    }
    else
    {
        cout << "Invalid choice." << endl;
    }
}