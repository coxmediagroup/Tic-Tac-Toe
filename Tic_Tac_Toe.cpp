#include<iostream>
#include<string>

using namespace std;

int main()
{
	int i, j, m, n, s=0;
	char a[3][3], p, p1[20]={'P','l','a','y','e','r','1'}, p2[20]={'P','l','a','y','e','r','2'}, c, sign=' ', winner=' ', spot;
	
	cout<<endl;
	cout<<"\t  Welcome to the Game"<<endl;
	cout<<"\t    Tick Tack Toe"<<endl<<endl<<"  Game has the following dimensions :"<<endl;                  //Game's instructions
	
	cout<<"  And you need to press number according to its place"<<endl<<endl;
	
	for(i=0; i<3; i++)
	{
		cout<<"    ";
		for(j=0; j<3; j++)
		{
			s+=1;                                                                         //Game's Format
			cout<<"   "<<s;
		}
		cout<<endl<<"      --- --- ---"<<endl;
	}
	
	for(i=0; i<3; i++)
	{
		for(j=0; j<3; j++)
		a[i][j] =' ';
	}
	
H : cout<<endl<<"  If you want to rename your player name, enter Y otherwise N : ";                        //Inputting player's name
	cin>>p;
	
    if(p=='Y' || p=='y')
	{
		cout<<endl<<"  Enter name of Player 1 : ";
		scanf("%s", p1);
		cout<<"  Enter name of Player 2 : ";
		scanf("%s", p2);
	}
	
	else if(p!='n' && p!='N')
	{
		cout<<endl<<"  Wrong Input!"<<endl<<"  Try again :)"<<endl<<endl;
		goto H;
	}
	
	s= 0;
	
	for(i=1; i<=9; i++)
	{
		
		if(i%2==0)
		{
		    cout<<endl<<"  "<<p2<<" :";
	        sign = 'X';
		}
		else
		{
		    cout<<endl<<"  "<<p1<<" :";
            sign = 'O';
		}
	R :	cout<<endl<<"  Enter Number of your spot for keeping '"<<sign<<"' sign : ";
		cin>>spot;
		
		if(spot=='1')
		{
			m=0;
			n=0;
			goto K;
		}
		else if(spot=='2')
		{
			m=0;
			n=1;
			goto K;
		}
		else if(spot=='3')
		{
			m=0;                                 //For better User Interface (UI) & simplier controls for the game
			n=2;
			goto K;
		}
		else if(spot=='4')
		{
			m=1;
			n=0;
			goto K;
		}
		else if(spot=='5')
		{
			m=1;
			n=1;
			goto K;
		}
		else if(spot=='6')
		{
			m=1;
			n=2;
			goto K;
		}
		else if(spot=='7')
		{
			m=2;
			n=0;
			goto K;
		}
		else if(spot=='8')
		{
			m=2;
			n=1;
			goto K;
		}
		else if(spot=='9')
		{
			m=2;
			n=2;
			goto K;
		}
		else
		{
			cout<<"  Wrong Input!"<<endl<<"  Try again :) "<<endl<<endl<<"  ";
			goto R;
		}
		
		
	K :	if(a[m][n]!=' ')
	    {
	    	cout<<endl<<"  Input already taken!"<<endl<<"  Try a different input :) "<<endl<<endl;
	    	goto R;
	    }
	    
		a[m][n] = sign;
				
		for(int k=0; k<3; k++)
	    {
		    cout<<"    ";
		
		    for(int l=0; l<3; l++)
		    cout<<"   "<<a[k][l];
		
		    cout<<endl<<"      --- --- ---"<<endl;
	    }
	    
	    if(i>4)
	    {
	    	for(int k=0; k<3; k++)
	    	{
	    		if(a[k][0]== 'X' && a[k][1]== 'X' && a[k][2]== 'X')
	    		{
	    			winner = a[k][1];
	    			goto result;
				}
				
				if(a[k][0]== 'O' && a[k][1]== 'O' && a[k][2]== 'O')
	    		{
	    			winner = a[k][1];
	    			goto result;
				}
				
				if(a[0][k]== 'X' && a[1][k]== 'X' && a[2][k]== 'X')
				{
	    			winner = a[1][k];
	    			goto result;
				}
				
				if(a[0][k]== 'O' && a[1][k]== 'O' && a[2][k]== 'O')
				{
	    			winner = a[1][k];
	    			goto result;
				}
		    }
			
			if(a[0][0]== 'X' && a[1][1]== 'X' && a[2][2]== 'X')
			{
	    		winner = a[1][1];
	    		goto result;
			}
				
		    if(a[0][0]== 'O' && a[1][1]== 'O' && a[2][2]== 'O')
			{
	    		winner = a[1][1];
	    		goto result;
			}
			
			if(a[0][2]== 'X' && a[1][1]== 'X' && a[2][0]== 'X')
			{
	    		winner = a[1][1];
	    		goto result;
			}
			
			if(a[0][2]== 'O' && a[1][1]== 'O' && a[2][0]== 'O')
			{
	    		winner = a[1][1];
	    		goto result;
			}
		}
	}
	
result: if(winner == 'O')
	    cout<<"  "<<p1<<" is the Winner :) ";
	
	else if(winner == 'X')                                                //Checking for the winner
	cout<<"  "<<p2<<" is the Winner :) ";
	
	else
	cout<<"  Match Draw ! :( ";
	
}
