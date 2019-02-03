import UIKit
import FLAnimatedImage
import Alamofire
import Firebase
import FirebaseFirestore

class LoadingVC: UIViewController {
    
    @IBOutlet weak var imageLoader: FLAnimatedImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let urlString = "https://www.cgsinc.com/sites/default/files/media/images/features_benefits/animat-cloudsync-grey%20transp.gif"
        let url = URL(string: urlString)!
        let imageData = try? Data(contentsOf: url)
        let imageData3 = FLAnimatedImage(animatedGIFData: imageData)
        imageLoader.animatedImage = imageData3
        
        
        let db = Firestore.firestore()
        
        //NEW
        let citiesRef = db.collection("profile").document("users").collection("coredata")
        
        citiesRef.order(by: "date", descending: true).limit(to: 1).getDocuments() { (querySnapshot, err) in
            
            var userAge = ""
            var userHeight = ""
            var userWeight = ""
            var userChol = ""
            var userSex = true
            var userFamily = true
            var userSmoker = true
            var userBeats = ""
            var userPalp = ""
            var userExmin = ""
            
            for document in querySnapshot!.documents {
                userBeats = document.get("avgb") as! String
                userChol = document.get("chol") as! String
                userPalp = document.get("palp") as! String
                userExmin = document.get("excmin") as! String
            }
            
            //KEEP GOING
            let inside = db.collection("profile")
            
            inside.getDocuments() { (querySnapshot, err) in
                
                for document in querySnapshot!.documents {
                    print(document.get("age"))
                    print("ffhhfhfhfhfhfh")
                    userAge = document.get("age") as! String
                    userHeight = document.get("height") as! String
                    userWeight = document.get("weight") as! String
                    
                    if (document.get("sex") as! Bool == true){
                        userSex = true
                    }else{
                        userSex = false
                    }
                    
                    if (document.get("family-history") as! Bool == true){
                        userFamily = true
                    }else{
                        userFamily = false
                    }
                    
                    if (document.get("smoking-5") as! Bool == true){
                        userSmoker = true
                    }else{
                        userSmoker = false
                    }
                    
                }
          
            //Every Value Gotten
            var url = "http://35.231.233.248:5000/?";
            url = url + "age=" + userAge
            url = url + "&palpitations=" + userPalp
            url = url + "&chol=" + userChol
            url = url + "&heartRate=" + userBeats
            url = url + "&exercise=" + userExmin
            url = url + "&weight=" + userWeight
            url = url + "&height=" + userHeight
            
            if userSmoker == true{
                url = url + "&smoking-5=True"
            }else{
                url = url + "&smoking-5=False"
            }
            
            if userSex == true{
                url = url + "&sex=True"
            }else{
                url = url + "&sex=False"
            }
            
            if userFamily == true{
                url = url + "&family-history=True"
            }else{
                url = url + "&family-history=False"
            }
            print(url)
            
            Alamofire.request(url).response { response in
                if let data = response.data, let results = String(data: data, encoding: .utf8){
                    print("Data: \(results)")
                    
                    let citiesRef = db.collection("profile").document("users").collection("coredata")
                    
                    citiesRef.order(by: "date", descending: true).limit(to: 1).getDocuments() { (querySnapshot, err) in
                        var doc = ""
                        for document in querySnapshot!.documents {
                            doc = document.documentID
                            break
                        }
                        
                        db.collection("profile").document("users").collection("coredata").document(doc).setData([
                            "result": results
                        ], merge: true) { err in
                            if let err = err {
                                print("Error writing document: \(err)")
                            } else {
                                print("Document successfully written!")
                                
                            }
                        }
                        
                    }
                    
                    let timer = Timer.scheduledTimer(timeInterval: 3.0, target: self, selector: #selector(self.timeToMoveOn), userInfo: nil, repeats: false)
                    
                    
                }
                
            }
        }
            
    }
                
        
    }
    
    
    @objc func timeToMoveOn() {
        self.performSegue(withIdentifier: "toResults", sender: self)
    }
        
        
}


