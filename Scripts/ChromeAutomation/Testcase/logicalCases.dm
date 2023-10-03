// Function 
i:int;
fn : () void {
  i = 4;
}

argFunc: (a:int, b:int, c:int) int{
  if(b){
    return a*c;
  }
  return a+c;
}

main: () void {
  i = 0;

  // WhileStmt
  while(i <= 1 and true){
    i++;
  }
  i = 5;
  while(i >= 2){
    i--;
  }

  // IfStmt
  if(i == 2){
    return 1;
  }

  // IfElseStmt
  if(i == 2){
    return 1;
  } else{
    return 0;
  }

  // CallStmt
  fn();
  argfunc(1, 2, 3);

}