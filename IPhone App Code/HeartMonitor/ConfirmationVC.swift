//
//  ConfirmationVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-03.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import FirebaseFirestore
import Alamofire
import Firebase
import Foundation

class ConfirmationVC: UIViewController {

    
    @IBOutlet weak var riskLbl: UILabel!
    @IBOutlet weak var footerLbl: UILabel!
    @IBOutlet weak var str1: UILabel!
    @IBOutlet weak var str2: UILabel!
    @IBOutlet weak var str3: UILabel!
    @IBOutlet weak var str4: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    
        let db = Firestore.firestore()
        
        let citiesRef = db.collection("profile").document("users").collection("coredata")
        citiesRef.order(by: "date", descending: true).limit(to: 1).getDocuments() { (querySnapshot, err) in
            
            var userEx = ""
            var userChol = ""
            var userBeats = ""
            var userPalp = ""
            var userResults = ""
            var userWeight = ""
            var userHeight = ""
            
            for document in querySnapshot!.documents {
                userResults = document.get("result") as! String
                userPalp = document.get("palp") as! String
                userChol = document.get("chol") as! String
                userEx = document.get("excmin") as! String
            }
            
            //Cont
            let inside = db.collection("profile")
            inside.getDocuments() { (querySnapshot, err) in
                
                for document in querySnapshot!.documents {
                    userWeight = document.get("weight") as! String
                    userHeight = document.get("height") as! String
                }
                
                //Cont
                if (userResults == "True"){
                    self.riskLbl.text = "Your Are At Risk"
                    self.footerLbl.text = "Please Contact A Doctor Urgently"
                }else{
                    self.riskLbl.text = "Looking Great!"
                    self.footerLbl.text = "Continue to take care of your health!"
                }
                
                let w:Int! = Int(userWeight)
                let h:Int! = Int(userHeight)
                
                var bmi = (w / ((h / 100)*(h / 100)))
                
                var url = "https://benjohns.lib.id/projectcor@dev/?"
                url = url + "palp=" + userPalp
                url = url + "&bmi=" + String(bmi)
                url = url + "&excmin=" + userEx
                url = url + "&chol=" + userChol
                
                print(url)
                Alamofire.request(url).response { response in
                    if let data = response.data, let results = String(data: data, encoding: .utf8){
                        
                        print(results)
                    
                        let res = results.components(separatedBy: ",")
                        
                        self.str1.text = res[0]
                        self.str2.text = res[1]
                        self.str3.text = res[2]
                        self.str4.text = res[3]

                        
                    }
                    
                }
                
            }
        }
        
    }//OVERRIDE
    
    @IBAction func done(_ sender: UIBarButtonItem) {
        
        performSegue(withIdentifier: "toHome", sender: self)
        
    }
    
}
