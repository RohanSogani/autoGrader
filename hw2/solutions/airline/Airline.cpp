//
// Airline.cpp
//
#include "Airline.h"
#include <iostream>
using namespace std;

Airline::Airline(int nA321, int nB777, int nB787):
  nAirplanes(nA321+nB777+nB787)
{
  airplaneList = new Airplane*[nAirplanes];

  for ( int i = 0; i < nA321; i++ )
    airplaneList[i] = new Airplane(10);
  for ( int i = nA321; i < nA321+nB777; i++ )
    airplaneList[i] = new Airplane(32);
  for ( int i = nA321+nB777; i < nA321+nB777+nB787; i++ )
    airplaneList[i] = new Airplane(40);

  for ( int i = 0; i < nAirplanes; i++ )
    cout << "Airplane " << i+1 << " maximum load "
         << airplaneList[i]->maxLoad() << endl;
}

void Airline::addShipment(int size)
{
  for ( int i = 0; i < nAirplanes; i++ )
  {
    if ( airplaneList[i]->addContainers(size) )
    {
      cout << size << " containers added to airplane " << i+1 << endl;
      return;
    }
  }
  cout << " could not fit " << size << " containers" << endl;
}

void Airline::printSummary(void)
{
  cout << "Summary:" << endl;
  for ( int i = 0; i < nAirplanes; i++ )
  {
    int current_load = airplaneList[i]->currentLoad();
    if ( current_load > 0 )
      cout << "airplane " << i+1 << " " << current_load << "/"
           << airplaneList[i]->maxLoad() << endl;
  }
}
