//
// testAircraft.cpp
//

#include "Aircraft.h"
#include <iostream>
using namespace std;

int main()
{
  Aircraft *p1 = Aircraft::makeAircraft('A', "D-AIMB");
  p1->setHours(1,100);
  p1->setHours(2,300);
  p1->setHours(3,600);
  p1->setHours(4,200);
  p1->print();
  p1->printSchedule();
  delete p1;

  Aircraft *p2 = Aircraft::makeAircraft('B', "N772SW");
  p2->setHours(1,7700);
  p2->setHours(2,300);
  p2->print();
  p2->printSchedule();
  delete p2;
}
