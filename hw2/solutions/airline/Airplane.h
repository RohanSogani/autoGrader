//
// Airplane.h
//
#ifndef AIRPLANE_H
#define AIRPLANE_H
class Airplane
{
  public:
    Airplane(int n);
    int maxLoad(void);
    int currentLoad(void);
    bool addContainers(int n);
  private:
    const int maxContainers;
    int numContainers;
};
#endif
