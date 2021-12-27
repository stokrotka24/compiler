#for i in $(seq 0 9); do
#   echo "$(python3.8 ../CompilerParser.py ../tests/testy_gebala/error$i.imp ./testy_gebala/error$i.txt 2> ./testy_gebala/error$i.txt)"
#done

for i in $(seq 1 2); do
   echo "$(python3.8 ../CompilerParser.py ../tests/my_tests/test$i.imp ./my_tests/test$i.mr)"
done