//
// Airplane.cpp
//

#include <iostream>
#include <stdexcept>
#include "Airplane.h"
using namespace std;

Airplane::Airplane(int n) : maxContainers(n), numContainers(0) {}

int Airplane::maxLoad(void)
{
  return maxContainers;
}

int Airplane::currentLoad(void)
{
  return numContainers;
}

bool Airplane::addContainers(int n)
{
  if ( n <= 0 )
    throw invalid_argument("must be positive");

  if ( numContainers + n <= maxContainers )
  {
    numContainers += n;
    return true;
  }
  else
  {
    return false;
  }
}
