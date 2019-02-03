//
//  CholesterolVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import FirebaseFirestore

class CholesterolVC: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBOutlet weak var newChol: UITextField!
    
    @IBAction func btnPress(_ sender: UIButton) {
        
        let db = Firestore.firestore()
     
        //New Chol
        db.collection("profile").document("users").setData([
            "chol": self.newChol.text,
            ], merge: true) { err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
                
            }
        }
        
        performSegue(withIdentifier: "toFinal", sender: self)

    }
    
    @IBAction func actionDismiss(sender: AnyObject) {
        self.dismiss(animated: true, completion: nil)
    }
    
    
    @IBAction func skipBtn(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: "toFinal", sender: self)
    }
    
}
