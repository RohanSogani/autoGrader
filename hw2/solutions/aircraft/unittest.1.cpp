#include "Aircraft.h"
#include <iostream>
#include <string>
using namespace std;


template<typename T>
void verify(T a, T b, string c)
{
  if (a != b) {
    std::cout << "incorrect value for "
              << c
              << ": received " << a << " expecting " << b
              << std::endl;
  }
}


#define check_spelling(t, fun, va, vb)                  \
  A380 a("A-XXXX");                                     \
  B737 b("B-YYYY");                                     \
  Aircraft *pA = Aircraft::makeAircraft('A', "A-XXXX"); \
  Aircraft *pB = Aircraft::makeAircraft('B', "B-YYYY"); \
  verify<t>(a.fun(),   va, "incorrect result for #1 A380 Aircraft::" #fun);  \
  verify<t>(b.fun(),   vb, "incorrect result for #2 B737 Aircraft::" #fun);  \
  verify<t>(pA->fun(), va, "incorrect result for #3 A380 Aircraft::" #fun);  \
  verify<t>(pB->fun(), vb, "incorrect result for #4 B737 Aircraft::" #fun);  \
  delete pA;                                            \
  delete pB;


#define check_consistence(t, fun)                       \
  A380 a("A-XXXX");                                     \
  B737 b("B-YYYY");                                     \
  Aircraft *pa = Aircraft::makeAircraft('A', "A-XXXX"); \
  Aircraft *pb = Aircraft::makeAircraft('B', "B-YYYY"); \
  verify<t>(a.fun(), pa->fun(), "inconsistent polymorphic results for A380 Aircraft::" #fun); \
  verify<t>(b.fun(), pb->fun(), "inconsistent polymorphic results for B737 Aircraft::" #fun); \
  delete pa;                                            \
  delete pb;


int main(int ac, char** av)
{
  if      (std::string(av[1]) == "1a") { // type
    check_consistence(string, type);
  }
  else if (std::string(av[1]) == "1b") { // type
    check_spelling(string, type, "Airbus A380", "Boeing B737");
  }
  else if (std::string(av[1]) == "2a") { // maxHours
    check_consistence(int, maxHours);
  }
  else if (std::string(av[1]) == "2b") { // maxHours
    check_spelling(int, maxHours, 750, 500);
  }
  else if (std::string(av[1]) == "3a") { // numEngines
    check_consistence(int, numEngines);
  }
  else if (std::string(av[1]) == "3b") { // numEngines
    check_spelling(int, numEngines, 4, 2);
  }
  else if (std::string(av[1]) == "4a") { // name
    throw 1; //check_consistence(string, name);
  }
  else if (std::string(av[1]) == "4b") { // name
    throw 1; //check_spelling(string, name, "A-XXXX", "B-YYYY");
  }
  else if (std::string(av[1]) == "5") { // setHours should not print
    Aircraft *p = Aircraft::makeAircraft('A', "D-AIMB");
    p->setHours(1,100);
    p->setHours(2,300);
    p->setHours(3,600);
    p->setHours(4,200);
    delete p;
  }
  else if (std::string(av[1]) == "6") { // setHours should support out of order assignment
    Aircraft *p = Aircraft::makeAircraft('A', "D-AIMB");
    p->setHours(4,200);
    p->setHours(1,400);
    p->setHours(3,200);
    p->setHours(2,300);
    delete p;
  }
  else if (std::string(av[1]) == "7") { // print is correct
    Aircraft *p1 = Aircraft::makeAircraft('A', "D-AIMB");
    p1->setHours(1,100);
    p1->setHours(2,600);
    p1->setHours(3,500);
    p1->setHours(4,200);
    p1->print();
    Aircraft *p2 = Aircraft::makeAircraft('B', "N772SW");
    p2->setHours(1,7700);
    p2->setHours(2,300);
    p2->print();
    delete p1;
    delete p2;
  }
  else if (std::string(av[1]) == "8") { // printSchedule is correct
    Aircraft *p1 = Aircraft::makeAircraft('A', "D-AIMB");
    p1->setHours(1,300);
    p1->setHours(2,300);
    p1->setHours(3,700);
    p1->setHours(4,200);
    p1->printSchedule();
    Aircraft *p2 = Aircraft::makeAircraft('B', "N772SW");
    p2->setHours(1,700);
    p2->setHours(2,900);
    p2->printSchedule();
    delete p1;
    delete p2;
  }
  else {
    throw 0;
  }

}
