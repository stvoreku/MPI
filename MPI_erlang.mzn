% Zaprojektuj algorytm orkiestracji usług dla systemu obliczeń na brzegu sieci,
% który pozwoli zagwarantować założony poziom dostępności usług oraz zapewni efektywne wykorzystanie zasobów.


% Liczba serwerów MEC
int: m;

% Liczba kontenerów (wszystkie są takie same)
var int: n;

% Zbiór serwerów
set of int: I = 1..m;

% Zbiór kontenerów
set of int: J = 1..max_cont_num;

% Zasoby zajmowane przez jeden kontener
int: a = 9;

% Tablica maksymalnych pojemności serwerów (i)
array[I] of int: b;

% Koszt alokacji kontenera na serwerze i
array[I] of int: c;

% Tablica zapotrzebowań przy serwerach
array[I] of float: z;

% Całkowite zapotrzebowanie
float: A = sum(z);

% Dopuszczalny poziom niedostępności
float: prob;

% Poszukiwany rozkład kontenrów: 
% x[i,j] = 1 oznacza że kontener j jest przypisany do serwera i  //tu można zmienić na więcej niż jeden może?
array[I,J] of var 0..1: x;

% Funkcja celu: jak najtaniej rozłożyć kontenery

var int: obj = sum(i in I, j in J) (c[i] * x[i,j]);

solve :: int_search( 
        [x[i,j] | i in I, j in J] ++ [obj] , 
        first_fail, indomain_min, complete)
    minimize obj;

constraint
  obj >= 0
  /\

  % Każdy kontener musi być przypisany do dokładnie jednego serwera
  forall(j in J) (sum(i in I) (x[i,j]) = 1)

  /\
  % Ilość zasobów przypisanych do każdego serwera i nie może przekroczyć jego pojemności
  forall(i in I) ( sum(j in J) (a * x[i,j]) <= (b[i]))

;

constraint block_prob(A, n) <= 1-prob;

output [
  "\nobj: ", show(obj), 

] ++
[
  if j = 1 then "\n" else " " endif ++
    show(x[i,j]) 
  | i in I, j in J
] ++ ["\n"] ++ ["some variable: ", show(m)];


% Erlang

% Maksymalna liczba kontenerów jaka może być w systemie
int: max_cont_num = sum(i in I) (ceil(b[i] / a));


function var float: block_prob(var float: A, var int: l) = 
  if l = 0 then 1 else a*block_prob(a, l-1) / (a*block_prob(a, l-1) + l) endif;



% Dane

prob = 0.05;

m = 5;
% n = 15;

b = [36,34,38,27,33];
%b = [35,35,35,35,35];

z = [1,2,1,3,2];

c = [17,21,22,18,24];