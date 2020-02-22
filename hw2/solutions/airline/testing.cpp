#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdexcept>
#include <string>
#include <vector>
#include <sstream>

#include "Airline.h"

using namespace std;

namespace ref {
  class AP {
  public:
    AP(int n) : maxContainers(n), numContainers(0) {}
    int maxLoad(void) { return maxContainers; }
    int currentLoad(void) { return numContainers; }
    bool addContainers(int n) {
      if (n <= 0)
	throw invalid_argument("must be positive");
      if (numContainers + n <= maxContainers) {
	  numContainers += n;
	  return true;
      }
      else { return false; }
    }
  private:
    const int maxContainers;
    int numContainers;
  };
  class AL {
  public:
    AL(int nA321, int nB777, int nB787): nAirplanes(nA321+nB777+nB787) {
      airplaneList = new AP*[nAirplanes];      
      for (int i = 0; i < nA321; i++)
	airplaneList[i] = new AP(10);
      for (int i = nA321; i < nA321+nB777; i++)
	airplaneList[i] = new AP(32);
      for (int i = nA321+nB777; i < nA321+nB777+nB787; i++ )
	airplaneList[i] = new AP(40);      
      for (int i = 0; i < nAirplanes; i++)
	cout << "Airplane " << i+1 << " maximum load "
	     << airplaneList[i]->maxLoad() << endl;
    }
    void addShipment(int size) {
      for (int i = 0; i < nAirplanes; i++) {
	if (airplaneList[i]->addContainers(size)) {
	  cout << size << " containers added to airplane " << i+1 << endl;
	  return;
	}
      }
      cout << " could not fit " << size << " containers" << endl;
    }
    void printSummary(void) {
      cout << "Summary:" << endl;
      for (int i = 0; i < nAirplanes; i++)
	{
	  int current_load = airplaneList[i]->currentLoad();
	  if (current_load > 0)
	    cout << "airplane " << i+1 << " " << current_load << "/"
		 << airplaneList[i]->maxLoad() << endl;
	}
    }    
  public:
    const int nAirplanes;
    AP** airplaneList;
  };
}

#define assert(x)					\
  if(!(x)) {						\
    throw std::runtime_error("failed assert: " #x);	\
  }							\
  
void test_except()
{
  bool valid = false;
  try {
    //    Airplane a(10);
    Airline b(1, 1, 1);
    //    try {
    //  a.addContainers(-100);
    //} catch (invalid_argument &e) { valid = true; }
    try {
      b.addShipment(-10);
    } catch (invalid_argument &e) { valid = true; }
  } catch (...) {}
  
  if (valid)
    return;

  throw std::runtime_error("Airplane does not throw for invalid arguments");
}

template<typename T>
void test_airline(int n1, int n2, int n3, std::vector<int>& input)
{
  T airline(n1, n2, n3);
  for (size_t i = 0; i < input.size(); ++i) {
    try {
      airline.addShipment(input[i]);
    }
    catch( invalid_argument &e ) {
      cerr << "Invalid shipment size: " << e.what() << " (skipped)" << endl;
    }
  }
  airline.printSummary();  
}

int main(int ac, char** av)
{
  srand(time(NULL));

  stringstream str;
  stringbuf* buf =  str.rdbuf();
  auto*     old = cout.rdbuf(buf);
  
  if      (string(av[1]) == "1") { // Airplane::except
    test_except();
  }
  else if (string(av[1]) == "2") { // Airplane::maxLoad
    Airplane a(10);
    assert(a.maxLoad() == 10);
  }
  else if (string(av[1]) == "3") { // Airplane::addContainer
    Airplane a(10);    
    assert(a.addContainers(5) == true);
    assert(a.addContainers(3) == true);
    assert(a.addContainers(8) == false);
  }
  else if (string(av[1]) == "4") { // Airplane::currentLoad
    Airplane a(10);
    try {
      a.addContainers(3);
      a.addContainers(5);
    } catch (...) { /* avoid duplicated errors */ }
    assert(a.currentLoad() == 8);
  }
  else if (string(av[1]) == "5") { // Airplane::currentLoad
    Airplane a(10);
    try {
      a.addContainers(3);
      a.addContainers(6);
      a.addContainers(8);
    } catch (...) { /* avoid duplicated errors */}
    assert(a.currentLoad() == 9);
  }
  else if (string(av[1]) == "6") { // Airline
    for (int x = 0; x < 30; ++x) {
      // input
      const int n1 = rand() % 20 + 1;
      const int n2 = rand() % 30 + 1;
      const int n3 = rand() % 40 + 1;    
      std::vector<int> items(20);
      for (size_t i = 0; i < items.size(); ++i) {
	items[i] = rand() % 10 + 1;
      }
      // run the test case
      try { test_airline<Airline>(n1, n2, n3, items); }
      catch (...) {}
      string s1 = str.str();
      str.str("");
      // run the reference case
      try { test_airline<ref::AL>(n1, n2, n3, items); }
      catch (...) {}
      string s2 = str.str();
      str.str("");
      // check
      assert(s1 == s2);
    }
  }

  cout.rdbuf(old);
  
  return 0;
}
