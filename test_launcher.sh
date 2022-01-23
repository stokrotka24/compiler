echo "0-div-mod.imp"
python3.8 kompilator.py tests/testy2021/0-div-mod.imp tests_results/testy2021/0-div-mod.mr
echo 1 0 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/0-div-mod.mr
echo "CR: 1 0 0 0"
read -p "Press enter ... " -n1 -s

echo "1-numbers.imp"
python3.8 kompilator.py tests/testy2021/1-numbers.imp tests_results/testy2021/1-numbers.mr
echo 12 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/1-numbers.mr
echo "CR: 0 1 -2 10 -100 10000 -1234567890 27 15 -999 -555555555 7777 -999 11 707 7777"
read -p "Press enter ... " -n1 -s

echo "2-fib.imp"
python3.8 kompilator.py tests/testy2021/2-fib.imp tests_results/testy2021/2-fib.mr
echo 1 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/2-fib.mr
echo "CR: 121393"
read -p "Press enter ... " -n1 -s

echo "3-fib-factorial.imp"
python3.8 kompilator.py tests/testy2021/3-fib-factorial.imp tests_results/testy2021/3-fib-factorial.mr
echo 20 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/3-fib-factorial.mr
echo "CR: 2432902008176640000 6765"
read -p "Press enter ... " -n1 -s

echo "4-factorial.imp"
python3.8 kompilator.py tests/testy2021/4-factorial.imp tests_results/testy2021/4-factorial.mr
echo 20 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/4-factorial.mr
echo "CR: 2432902008176640000"
read -p "Press enter ... " -n1 -s

echo "5-tab.imp"
python3.8 kompilator.py tests/testy2021/5-tab.imp tests_results/testy2021/5-tab.mr
maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/5-tab.mr
echo "CR: 0 ... 0 "
read -p "Press enter ... " -n1 -s

echo "6-mod-mult.imp"
python3.8 kompilator.py tests/testy2021/6-mod-mult.imp tests_results/testy2021/6-mod-mult.mr
echo 1234567890  1234567890987654321 987654321 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/6-mod-mult.mr
echo "CR: 674106858"
read -p "Press enter ... " -n1 -s

echo "7-loopiii.imp"
python3.8 kompilator.py tests/testy2021/7-loopiii.imp tests_results/testy2021/7-loopiii.mr
echo 0 0 0 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/7-loopiii.mr
echo "CR: 31000 40900 2222010"
echo 1 0 2 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/7-loopiii.mr
echo "CR: 31001 40900 2222012"
read -p "Press enter ... " -n1 -s

echo "8-for.imp"
python3.8 kompilator.py tests/testy2021/8-for.imp tests_results/testy2021/8-for.mr
echo 12 23 34 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/8-for.mr
echo "CR: 507 4379 0"
read -p "Press enter ... " -n1 -s

echo "9-sort.imp"
python3.8 kompilator.py tests/testy2021/9-sort.imp tests_results/testy2021/9-sort.mr
maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/9-sort.mr
echo "CR: 1 .. 22"
read -p "Press enter ... " -n1 -s

echo "div-mod.imp"
python3.8 kompilator.py tests/testy2021/div-mod.imp tests_results/testy2021/div-mod.mr
echo 26 7| maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/div-mod.mr
echo "CR:
   > 3
   > 5
   > -4
   > -2
   > 3
   > -5
   > -4
   > 2"
read -p "Press enter ... " -n1 -s

echo "program0.imp"
python3.8 kompilator.py tests/testy2021/program0.imp tests_results/testy2021/program0.mr
echo 34 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/program0.mr
echo "CR:
> 0
> 1
> 0
> 0
> 0
> 1"
read -p "Press enter ... " -n1 -s

echo "program1.imp"
python3.8 kompilator.py tests/testy2021/program1.imp tests_results/testy2021/program1.mr
maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/program1.mr
read -p "Press enter ... " -n1 -s

echo "program2.imp"
python3.8 kompilator.py tests/testy2021/program2.imp tests_results/testy2021/program2.mr
echo 1234567890 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/program2.mr
echo "CR:
> 2
> 1
> 3
> 2
> 5
> 1
> 3607
> 1
> 3803
> 1"
echo 12345678901 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/program2.mr
echo "CR:
> 857
> 1
> 14405693
> 1"
echo 12345678903 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy2021/program2.mr
echo "CR:
> 3
> 1
> 4115226301
> 1"
read -p "Press enter ... " -n1 -s

for f in $(find tests/testy_gebala -type f -name "error*.imp") ; do
    echo -e "\n$f"
    sed "/)/q" $f
    python3.8 kompilator.py $f out.mr
    echo
    read -p "Press enter ... " -n1 -s
    echo
done

echo "test0.imp"
python3.8 kompilator.py tests/testy_slowik/test0.imp tests_results/testy_slowik/test0.mr
echo 1 -1 1 -1 1 -1 1 -1 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy_slowik/test0.mr
echo "CR: 1"
read -p "Press enter ... " -n1 -s

echo "test1a.imp"
python3.8 kompilator.py tests/testy_slowik/test1a.imp tests_results/testy_slowik/test1a.mr
echo 3 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy_slowik/test1a.mr
echo "CR: 4"
read -p "Press enter ... " -n1 -s

echo "test1b.imp"
python3.8 kompilator.py tests/testy_slowik/test1b.imp tests_results/testy_slowik/test1b.mr
echo 3 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy_slowik/test1b.mr
echo "CR: 4"
read -p "Press enter ... " -n1 -s

echo "test1c.imp"
python3.8 kompilator.py tests/testy_slowik/test1c.imp tests_results/testy_slowik/test1c.mr
echo 3 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy_slowik/test1c.mr
echo "CR: 4"
read -p "Press enter ... " -n1 -s

echo "test1d.imp"
python3.8 kompilator.py tests/testy_slowik/test1d.imp tests_results/testy_slowik/test1d.mr
echo 3 | maszyna_wirtualna/maszyna-wirtualna tests_results/testy_slowik/test1d.mr
echo "CR: 4"
read -p "Press enter ... " -n1 -s

echo "test2.imp"
python3.8 kompilator.py tests/testy_slowik/test2.imp tests_results/testy_slowik/test2.mr
echo "CR:
  2^3
  3
  5^2
  7
  13
  41
  61
  641
  1321
  6700417
  613566757
  715827883"
maszyna_wirtualna/maszyna-wirtualna-cln tests_results/testy_slowik/test2.mr
read -p "Press enter ... " -n1 -s
