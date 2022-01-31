% Zaprojektuj algorytm orkiestracji usług dla systemu obliczeń na brzegu sieci,
% który pozwoli zagwarantować założony poziom dostępności usług oraz zapewni efektywne wykorzystanie zasobów.

% Wygenerowana wcześniej tablica dla wybranego m oraz b
include "erlangtable.dzn";
int: E_INDEX;
set of int: E_ = 1..E_INDEX-1;
array[E_] of float: ERLANG_TABLE;

% Dostępność wyrażona w procencie odrzuconych zapytań
float: max_block_rate;

% Liczba serwerów MEC
int: m;

%Liczba zadań / aplikacji
int: n;

% Indeksy serwerów
set of int: I = 1..m;

% Indeksy zadań
set of int: J = 1..n;

% Tablica zużycia zasobów zadania j na serwerze i (uwzględnia lokalizację)
array[I,J] of int: a; 

% Pojemność serwera MEC (wszystkie są takie same)
int: b;

% Tablica kosztów uruchomienia zadania j na serwerze i (uwzględnia lokalizację?)
array[I,J] of int: c;

% Poszukiwany rozkład kontenrów: 
% x[i,j] = 1 oznacza że kontener j jest przypisany do serwera i
array[I,J] of var 0..1: x;

% Jak najtaniej przypisać zadania
var int: obj = sum(i in I, j in J) (c[i,j] * x[i,j]);

var int: A_total = sum(i in I) ( sum(j in J) (a[i,j] * x[i,j])); % dzielenie przez b zostało uwzględnione w tablicy


var float: erlang = ERLANG_TABLE[A_total];

solve :: int_search( 
        [x[i,j] | i in I, j in J] ++ [obj] , 
        first_fail, indomain_min, complete)
    minimize obj;
    % maximize obj;

constraint
  obj >= 0
  /\

  % Każdy kontener musi być przypisany do dokładnie jednego serwera
  forall(j in J) (sum(i in I) (x[i,j]) = 1)

  /\
  % Ilość zasobów przypisanych do każdego serwera i nie może przekroczyć jego możliwości
  forall(i in I) ( sum(j in J) (a[i,j] * x[i,j]) <= b)
  
  /\
  erlang <= max_block_rate

;

output   ["\nerl: ", show(erlang), 
 
] ++ [
  "\nobj: ", show(obj), 
 
] ++
[
  if j = 1 then "\n" else " " endif ++
    show(x[i,j]) 
  | i in I, j in J
] ++ ["\n"];

% Dane

max_block_rate = 0.1;
m = 5;
n = 15;

a = array2d(I,J, [
 8,15,14,23, 8,16, 8,25, 9,17,25,15,10, 8,24,
15, 7,23,22,11,11,12,10,17,16, 7,16,10,18,22,
21,20, 6,22,24,10,24, 9,21,14,11,14,11,19,16,
20,11, 8,14, 9, 5, 6,19,19, 7, 6, 6,13, 9,18,
 8,13,13,13,10,20,25,16,16,17,10,10, 5,12,23]);

b = 120;

c = array2d(I, J,[
17,21,22,18,24,15,20,18,19,18,16,22,24,24,16,
23,16,21,16,17,16,19,25,18,21,17,15,25,17,24,
16,20,16,25,24,16,17,19,19,18,20,16,17,21,24,
19,19,22,22,20,16,19,17,21,19,25,23,25,25,25,
18,19,15,15,21,25,16,16,23,15,22,17,19,22,24]);