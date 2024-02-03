#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main()
{
    string input;
    int input2;

    cout << "Welcome to the Y Recover Center!" << endl;
    cout << "Please enter your username: ";
    cin >> input;
    transform(input.begin(), input.end(), input.begin(), ::tolower);
    if (input == "peter_lee")
    {
        cout << "Welcome, @Peter_Lee!" << endl;
        cout << "You've set 3 recovery questions before." << endl;
        cout << "They are:" << endl;
        cout << "  1. What is your favorite color?" << endl;
        cout << "  2. What is your mother's full name?" << endl;
        cout << "  3. What is your sister's birthday?" << endl;
        cout << "Please choose one: [ ]\b\b";
        cin >> input2;
        if (input2 == 1)
        {
            cout << "Please answer: What is your favorite color?" << endl;
            cin >> input;
            cout << "\033[31mWrong answer.\033[0m" << endl;
        }
        else if (input2 == 2)
        {
            cout << "Please answer: What is your mother's full name?" << endl;
            cin >> input;
            cout << "\033[31mWrong answer.\033[0m" << endl;
        }
        else if (input2 == 3)
        {
            cout << "Please answer: What is your sister's birthday? (in the format of 2024-01-01)" << endl;
            cin >> input;
            if (input == "1998-02-03")
            {
                cout << "\033[32mCorrect Answer!\033[0m" << endl;
                cout << "Please enter your new password:" << endl;
                cin >> input;
                cout << "Password updated successfully, please keep it safe!" << endl;
                cout << "==================================================="  << endl;
                cout << "Username: Peter_Lee" << endl;
                cout << "Password: ***" << endl;
                cout << "Email: great_peter_lee@qmail.com" << endl;
                cout << "==================================================="  << endl;
            }
            else
            {
                cout << "\033[31mWrong answer.\033[0m" << endl;
            }
        }
        else
        {
            cout << "Invalid choice." << endl;
        }
    }
    else
    {
        cout << "Sorry, account not found." << endl;
    }
}
