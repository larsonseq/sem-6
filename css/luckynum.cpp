#include<iostream>

int main() {
    std::string s;
    std::cin >> s;

    int count{0};
    
    for (int i = 0; i < s.length(); i++) {
        if (s[i] != '4' && s[i] != '7') { 
            std::cout << "NO\n";
            return 0;
        }
    }

    if (s.length() == 4 || s.length() == 7) {
        std::cout << "YES\n";
    }
    else {
        std::cout << "NO\n";
    }

    return 0;
}