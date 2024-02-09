#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void main_page();

int main()
{
    string input;

    cout << "Welcome to the Q-MAIL Recover Center!" << endl;
    cout << "QMail is better then all, especially those who matched /.+@[gG]mail.com/" << endl;
    cout << endl;
    cout << "Please enter your username (e.g. admin@qmail.com): ";
    cin >> input;
    transform(input.begin(), input.end(), input.begin(), ::tolower);
    if (input == "great_peter_lee@qmail.com")
    {
        cout << "Welcome!" << endl;
        cout << "You've set 1 recovery question(s)." << endl;
        cout << endl;
        cout << "What is your sister's birthday?" << endl;
        cout << "Please answer: (in the format of 2024-01-01)" << endl;
        cin >> input;
        if (input == "1998-02-03")
        {
            cout << "\033[32mCorrect Answer!\033[0m" << endl;
            cout << endl;
            cout << "Please enter your new password:" << endl;
            cin >> input;
            cout << "\033[32mPassword updated successfully, please keep it safe!\033[0m" << endl;
            cout << endl;
            cout << endl;
            main_page();
        }
        else
        {
            cout << "\033[31mWrong answer.\033[0m" << endl;
        }
    }
    else
    {
        cout << "\033[31mInvalid username.\033[0m" << endl;
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
        cout << endl << endl;
        cout << "\033[33m * (1 new email) *\033[0m" << endl;
        cout << "============================================" << endl;
        cout << "\033[90mFROM    : great_peter_lee@qmail.com\033[0m" << endl;
        cout << "\033[90mTO      : great_peter_lee@qmail.com\033[0m" << endl;
        cout << "\033[90mSubject : A little note            \033[0m" << endl;
        cout << "\033[90mDate    : 2024-01-01 00:00:00      \033[0m" << endl;
        cout << "============================================" << endl;
        cout << "Hello Peter," << endl;
        cout << "Here noted your passwords:" << endl;
        cout << "-----------------------------------------" << endl;
        cout << "|      Website     |      Password       |" << endl;
        cout << "| qmail.com        | plee666@qmail       |" << endl;
        cout << "| y.com            | plee666@y           |" << endl;
        cout << "| moz://b          | plee666@mozillb     |" << endl;
        cout << "| live.bighard.com | plee666@bighard     |" << endl;
        cout << "| unhackable       | ***                 |" << endl;
        cout << "-----------------------------------------" << endl;
        cout << "Please keep it safe and NEVER FORGET!" << endl;
        cout << "                                      Yours," << endl;
        cout << "                                   Peter Lee" << endl;
        cout << "============================================" << endl;
    }
    else
    {
        cout << "\033[31mInvalid choice.\033[0m" << endl;
    }
}