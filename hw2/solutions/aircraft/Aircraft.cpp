//
// Aircraft.cpp
//

#include <iostream>
#include <string>
#include "Aircraft.h"
using namespace std;

Aircraft::Aircraft(int n, string name_str): 
  numEng(n), nm(name_str), hrs(new int[numEng])
{
  for ( int i = 0; i < numEng; i++ )
    hrs[i] = 0; 
}

Aircraft::~Aircraft()
{
  delete [] hrs;
}

const string Aircraft::name() const
{
  return nm;
}

// Engines are numbered starting at 1
void Aircraft::setHours(int i, int h)
{ hrs[i-1] = h; }

int Aircraft::numEngines(void) const { return numEng; }

void Aircraft::print() const
{
  cout << "Aircraft: " << name() << " type: " << type() 
       << " has " << numEng << " engines" << endl;
  for ( int i = 0; i < numEng; i++ )
    cout << "engine " << i+1 << ": " << hrs[i] << " hours" << endl;
}

void Aircraft::printSchedule() const
{
  cout << "Maintenance schedule for " << name() << endl;
  for ( int i = 0; i < numEng; i++ )
  {
    cout << "engine " << i+1 << ": maintenance due ";
    int time = maxHours() - hrs[i];
    if ( time > 0 )
      cout << "in " << time << " hours" << endl;
    else
      cout << "now!!" << endl;
  }
}

Aircraft* Aircraft::makeAircraft(char ch, string name_str)
{
  if ( ch == 'A' )
  {
    // create an A380
    return new A380(name_str);
  }
  else if ( ch == 'B' )
  {
    // create a B737
    return new B737(name_str);
  }
  else
  {
    return 0;
  }
}

A380::A380(string name_str) : Aircraft(4,name_str) {}
const string A380::type(void) const { return "Airbus A380"; }
const int A380::maxHours(void) const { return 750; }

B737::B737(string name_str) : Aircraft(2,name_str) {}
const string B737::type(void) const { return "Boeing B737"; }
const int B737::maxHours(void) const { return 500; }
