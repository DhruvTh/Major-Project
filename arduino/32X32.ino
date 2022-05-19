
const byte M11 = 4;   
const byte M12 = 5; 
const byte M13 = 6; 
const byte M14 = 7;
const byte M21 = 8;  
const byte M22 = 9; 
const byte M23 = 10; 
const byte M24 = 11;
const byte D11 = 14;  
const byte D12 = 15; 
const byte D13 = 16; 
const byte D14 = 17;
const byte D21 = 18;  
const byte D22 = 19; 
const byte D23 = 20; 
const byte D24 = 21;

//Mux in "SIG" pin default for arduino mini pro  
const byte SIG_pin1 = A1;
const byte SIG_pin2 = A2;
//Mux out "SIG" pin default for arduino mini pro 
const byte OUT_pin1 = 2;
const byte OUT_pin2 = 3;

const boolean muxChannel[32][4]={
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1},  //channel 15
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1}  //channel 15
  };


//incoming serial byte

int valor = 0;               //variable for sending bytes to processing
int calibra[32][32];         //Calibration array for the min values of each od the 225 sensors.
int matrix[32][32];
int minsensor=1024;          //Variable for staring the min array

void setup(){  
  pinMode(M11, OUTPUT); 
  pinMode(M12, OUTPUT); 
  pinMode(M13, OUTPUT); 
  pinMode(M14, OUTPUT); 
  pinMode(M21, OUTPUT); 
  pinMode(M22, OUTPUT); 
  pinMode(M23, OUTPUT); 
  pinMode(M24, OUTPUT);
  pinMode(D11, OUTPUT); 
  pinMode(D12, OUTPUT); 
  pinMode(D13, OUTPUT); 
  pinMode(D14, OUTPUT);
  pinMode(D21, OUTPUT); 
  pinMode(D22, OUTPUT); 
  pinMode(D23, OUTPUT); 
  pinMode(D24, OUTPUT);
  pinMode(OUT_pin1, OUTPUT);
  pinMode(OUT_pin2, OUTPUT); 
  pinMode(SIG_pin1, INPUT);
  pinMode(SIG_pin2, INPUT); 
  
  digitalWrite(M11, LOW);
  digitalWrite(M12, LOW);
  digitalWrite(M13, LOW);
  digitalWrite(M14, LOW);
  digitalWrite(M21, LOW);
  digitalWrite(M22, LOW);
  digitalWrite(M23, LOW);
  digitalWrite(M24, LOW);
  digitalWrite(D11, LOW);
  digitalWrite(D12, LOW);
  digitalWrite(D13, LOW);
  digitalWrite(D14, LOW);
  digitalWrite(D21, LOW);
  digitalWrite(D22, LOW);
  digitalWrite(D23, LOW);
  digitalWrite(D24, LOW);
  digitalWrite(OUT_pin1, HIGH);
  digitalWrite(OUT_pin2, HIGH);
  Serial.begin(19200);
  
  Serial.println("\nCalibrating...\n");
  // Full of 0's of initial matrix
  for(byte j = 0; j < 32; j ++){ 
    for(byte i = 0; i < 32; i ++){
      calibra[j][i] = 0;
      matrix[j][i]= 0;}
  }
  // Calibration
  for(byte k = 0; k < 50; k++){  
    for(byte j = 0; j < 32; j ++){ 
      writeMux(j);
      for(byte i = 0; i < 32; i ++)
        calibra[j][i] = calibra[j][i] + readMux(i);
    }
  }
  
  //Print averages
  for(byte j = 0; j < 32; j ++){ 
    for(byte i = 0; i < 32; i ++){
      calibra[j][i] = calibra[j][i]/50;
      if(calibra[j][i] < minsensor)
        minsensor = calibra[j][i];
      matrix[j][i] = calibra[j][i];
      Serial.print(calibra[j][i]);
      Serial.print("\t");
    }
  Serial.println(); 
  }
  Serial.println();
  Serial.print("Minimum Value: ");
  Serial.println(minsensor);
  Serial.println();
}


void loop(){
  Serial.println("Data");
  for(int j = 0; j <32; j++){ 
    writeMux(j);
    for(int i = 0; i < 32; i++){
      valor = readMux(i);
      //Saturation sensors
      int limsup = 1024;
      valor=valor-calibra[j][i];
      if(valor > limsup)
       valor = limsup;
       if(valor < minsensor)
        valor = minsensor;  
       valor = map(valor,minsensor, limsup,0,300); 
       matrix[j][i]=valor;
       Serial.println(matrix[j][i]);
       //Serial.print("\t");
       }
       //Serial.println(); 
   }
}
        


int readMux(byte channel){
  if( channel < 16 ){
   byte controlPin[] = {M11, M12, M13, M14};
   for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);}
    int val = analogRead(SIG_pin1);
   return val;}
  if( channel > 15 ){
   byte controlPin[] = {M21, M22, M23, M24};
   for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);}
    int val = analogRead(SIG_pin2);
   return val;}
}

void writeMux(byte channel){
  if( channel < 16 ){
  byte controlPin[] = {D11, D12, D13, D14};
  for(byte i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }}
  if( channel > 15 ){
  byte controlPin[] = {D21, D22, D23, D24};
  for(byte i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }}
}
