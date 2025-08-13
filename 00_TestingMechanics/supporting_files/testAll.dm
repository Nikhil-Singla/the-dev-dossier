// Global Declaration and Type
myInt: int;
myBool: bool;
myPerfectInt: perfect int;
myPerfectBool: perfect bool;

// Function 
i:int;
fn : () void {
  i = 4;
}

// ClassDefn
myClass : class {
  a: int;
};

// Function with arguments
argFunc: (a:int) int{
  if(b){
    return a*c;
  }
  return a+c;
}

argFunc: (a:int, b:int, c:int) int{
  if(b){
    return a*c;
  }
  return a+c;
}

// blockStmt
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

  // MemberFieldExp
  myClass--a = 0;

  // BinaryExpression
  i = i+i;
  i = i*i;
  i = i/i;
  i = i-i;

  // UnaryExpression
  i = !i;
  i = -i;

  // declaration inside function
  myInt: int = 1;
  myBool: bool = true;
  myPerfectInt: perfect int;
  myPerfectBool: perfect bool;

  // unique keywords
  myMagic: magic = 24Kmagic;
  take a;
	give 2+2;
  myHot: bool = too hot;
  today I don't feel like doing any work;

  a: myClass;
 
  return;
}