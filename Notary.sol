ragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//evault solidity code
contract Notary {

    uint public userCount = 0; 
    mapping(uint => user) public userList; 
     struct user
     {
       string username;
       string password;
       string phone;
       string email;
       string home_address;      
     }
 
   // events 
   event userCreated(uint indexed _userId);
   
   //function  to save user details to Blockchain
   function saveUser(string memory uname, string memory pass, string memory phone, string memory emailid, string memory homes_address) public {
      userList[userCount] = user(uname, pass, phone, emailid, homes_address);
      emit userCreated(userCount);
      userCount++;
    }

     //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    uint public notaryCount = 0; 
    mapping(uint => notary) public notaryList; 
     struct notary
     {
       string username;
       string filename;
       string hash;   
       string signature;
       string date;
       string key;
     }
 
   // events 
   event notaryCreated(uint indexed _nId);
   
   //function  to save notary details to Blockchain
   function RegisterHash(string memory uname, string memory fname, string memory ha, string memory sig, string memory dd, string memory k) public {
      notaryList[notaryCount] = notary(uname, fname, ha, sig, dd, k);
      emit notaryCreated(notaryCount);
      notaryCount++;
    }
   //function to delete keys
    function deleteKey(uint i) public { 
      notaryList[i].hash = "Delete";
   }

    //get notary count
    function getNotaryCount()  public view returns (uint) {
          return notaryCount;
    }

   function getUsername(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.username;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.password;
    }

    function getPhone(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.phone;
    }

   
    function getEmail(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.email;
    }

    function getAddress(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.home_address;
    }

     function getHashcode(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.hash;
    }

    function getOwner(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.username;
    }

    function getFilename(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.filename;
    }

    function getSignature(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.signature;
    }

    function getDate(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.date;
    }    

    function getKey(uint i) public view returns (string memory) {
        notary memory nl = notaryList[i];
	return nl.key;
    }    
}
