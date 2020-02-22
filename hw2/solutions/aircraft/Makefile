CXXFLAGS = -Wall

all: maintenance testAircraft

maintenance: maintenance.o Aircraft.o
	@$(CXX) -o $@ $^

testAircraft: testAircraft.o Aircraft.o
	@$(CXX) -o $@ $^

unittest: unittest.o Aircraft.o
	@$(CXX) -o $@ $^

clean:
	@rm -f maintenance testAircraft unittest *.o
