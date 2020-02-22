CXXFLAGS = -Wall $(WARNING_AS_ERROR)

assignshipments: assignshipments.o Airline.o Airplane.o
	$(CXX) -o $@ $^

testing: testing.o Airline.o Airplane.o
	$(CXX) -o $@ $^

.o: .c
	$(CXX) -o $@ $^

clean:
	rm -f *.o assignshipments
