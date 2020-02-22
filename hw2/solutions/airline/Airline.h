//
// Airline.h
//
#ifndef AIRLINE_H 
#define AIRLINE_H
#include "Airplane.h"
class Airline 
{
  public:
  Airline(int nA321, int nB777, int nB787);
  void addShipment(int size);
  void printSummary(void);

  private:
  const int nAirplanes;
  Airplane** airplaneList;
};
#endif
