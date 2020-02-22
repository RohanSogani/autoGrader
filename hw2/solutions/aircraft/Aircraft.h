//
// Aircraft.h
//
#ifndef AIRCRAFT_H
#define AIRCRAFT_H
#include<string>

class Aircraft
{
  public:
    Aircraft(int n, std::string name_str);
    virtual const std::string type(void) const = 0;
    virtual const int maxHours(void) const = 0;
    const std::string name(void) const;
    int numEngines(void) const;
    void setHours(int i, int h);
    void print(void) const;
    void printSchedule(void) const;
    static Aircraft* makeAircraft(char ch, std::string name_str);
    virtual ~Aircraft(void);
  protected:
    const int numEng;
    const std::string nm;
    int* hrs;
};

class A380: public Aircraft
{
  public:
    A380(std::string name_str);
    virtual const std::string type(void) const;
    virtual const int maxHours(void) const;
};

class B737: public Aircraft
{
  public:
    B737(std::string name_str);
    virtual const std::string type(void) const;
    virtual const int maxHours(void) const;
};
#endif
