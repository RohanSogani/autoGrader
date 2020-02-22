//
// maintenance.cpp
//

#include "Aircraft.h"
#include <iostream>
using namespace std;

int main()
{
  char ch;
  string s;
  cin >> ch >> s;
  while ( cin )
  {
    Aircraft *p = Aircraft::makeAircraft(ch,s);
    if ( p != 0 )
    {
      for ( int i = 1; i <= p->numEngines(); i++ )
      {
        int h;
        cin >> h;
        p->setHours(i,h);
      }      

      p->print();
      p->printSchedule();
      cin >> ch >> s;
    }
    else
    {
      cout << "unknown aircraft code" << endl;
      return 1;
    }
  }
}
