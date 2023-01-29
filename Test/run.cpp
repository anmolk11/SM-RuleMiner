#include<bits/stdc++.h>
using namespace std;

fstream wrt,rd;

void write(vector<double> args){
    wrt.open("in.txt",ios::out);
    int N = args.size();

    for(int i = 0;i < N;i++){
        wrt<<args[i]<<'\n';
    }
}

vector<double> F(int id){
    vector<double> args1 = {

    };
    vector<double> args2 = {

    };
    vector<double> args3 = {

    };
    vector<double> args4 = {

    };

    return args1;
}


int main(){
    for(int i = 1;i <= 4;i++){
        write(F(i));
        system("python redo.py");
    }
}