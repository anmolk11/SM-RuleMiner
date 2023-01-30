#include<bits/stdc++.h>
using namespace std;

fstream wrt,rd;

void write(vector<double> args){
    wrt.open("in.txt",ios::out);
    int N = args.size();

    for(int i = 0;i < N;i++){
        wrt<<args[i]<<'\n';
    }
    wrt.close();
}

vector<double> F(int id){
    vector<vector<double>> args={
        {
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,19.27,96.28,0,0,0,0,0,0
        },
        {
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0.36,2.0,1,23,74
        },
        {
        0,0,0,1,95,179,0,0,0,0,0,0,0,0,0,1,31.7,58.16,0,0,0,0,0,0
        },
        {
        0,0,0,0,0,0,0,0,0,1,32,95,0,0,0,0,0,0,0,0,0,0,0,0
        }
    };
    return args[id]; 
}


int main(){
    for(int i = 0;i < 4;i++){
        write(F(i));
        system("python redo.py");
        rd.open("Flag.txt",ios::in);
        string ok;
        rd>>ok;
        rd.close();
        if(ok == "0") break;
    }
}