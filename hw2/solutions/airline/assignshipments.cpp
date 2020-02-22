//
// assignshipments.cpp
//

#include <iostream>
#include "Airline.h"
using namespace std;

int main(void)
{
  // create an Airline with 4 A321, 2 B777 and 1 B787
  Airline airline(4,2,1);

  do
  {
    try
    {
      int shipment_size = 0;
      cin >> shipment_size;
      if ( cin )
      {
        cout << "Trying to assign shipment of " << shipment_size
             << " containers" << endl;
        airline.addShipment(shipment_size);
      }
    }
    catch( invalid_argument &e )
    {
      cout << "Invalid shipment size: " << e.what() << " (skipped)" << endl;
    }
  }
  while ( cin );

  airline.printSummary();
}
