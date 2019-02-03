//
//  AddDataVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import FirebaseFirestore
import Firebase

class AddDataVC: UIViewController {

    @IBOutlet weak var daysWorked: UITextField!
    @IBOutlet weak var userWeight: UITextField!
    @IBOutlet weak var userHeight: UITextField!
    @IBOutlet weak var userBeats: UITextField!
    @IBOutlet weak var userPalp: UITextField!
    @IBOutlet weak var userChol: UITextField!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let db = Firestore.firestore()
        
        //Read
        let docRef = db.collection("profile").document("users")
       
        docRef.getDocument { (document, error) in
            if let document = document, document.exists {
                
                self.userWeight.text = document.get("weight") as! String
                self.userHeight.text = document.get("height") as! String
                self.userChol.text = document.get("chol") as! String
            
            } else {
                print("Document does not exist")
            }
        }
       
    }
    
    @IBAction func submitBtn(_ sender: UIBarButtonItem) {
        
        let db = Firestore.firestore()
        
        //UPDATE PROFILE
        db.collection("profile").document("users").setData([
            "chol": self.userChol.text,
            "height": self.userHeight.text,
            "weight": self.userWeight.text
        ], merge: true) { err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
                
            }
        }
    
        //Update Core Date
        db.collection("profile").document("users").collection("coredata").document().setData([
            "date": "\(Timestamp)",
            "chol": self.userChol.text,
            "palp": self.userPalp.text,
            "avgb": self.userBeats.text,
            "excmin": self.daysWorked.text
        ]) { err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
                
            }
        }
    
        performSegue(withIdentifier: "toFinal", sender: self)
        
    }
   
    var Timestamp: String {
        return "\(NSDate().timeIntervalSince1970 * 1000)"
    }
    
    @IBAction func actionDismiss(sender: AnyObject) {
        self.dismiss(animated: true, completion: nil)
    }


}
