//
//  ProfileVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import Firebase
import FirebaseFirestore

class ProfileVC: UIViewController {
    
    //Loading elements
    @IBOutlet weak var userImage: UIImageView!
    @IBOutlet weak var userName: UILabel!
    @IBOutlet weak var userEmail: UILabel!
    @IBOutlet weak var userSex: UISegmentedControl!
    @IBOutlet weak var userAge: UITextField!
    @IBOutlet weak var userPhone: UITextField!
    @IBOutlet weak var userSmoker: UISegmentedControl!
    @IBOutlet weak var userFamily: UISegmentedControl!
    @IBOutlet weak var userChol: UITextField!
    @IBOutlet weak var userWeight: UITextField!
    @IBOutlet weak var userSize: UITextField!
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        let db = Firestore.firestore()
        
        let docRef = db.collection("profile").document("users")
        
        docRef.getDocument { (document, error) in
            if let document = document, document.exists {
                
                self.userWeight.text = document.get("weight") as! String
                self.userAge.text = document.get("age") as! String
                self.userPhone.text = document.get("phone") as! String
                self.userSize.text = document.get("height") as! String
                self.userChol.text = document.get("chol") as! String
                
                if (document.get("sex") as! Bool == true){
                    self.userSex.selectedSegmentIndex = 0
                }else{
                    self.userSex.selectedSegmentIndex = 1
                }
                
                if (document.get("family-history") as! Bool == true){
                    self.userFamily.selectedSegmentIndex = 0
                }else{
                    self.userFamily.selectedSegmentIndex = 1
                }
                
                if (document.get("smoking-5") as! Bool == true){
                    self.userSmoker.selectedSegmentIndex = 0
                }else{
                    self.userSmoker.selectedSegmentIndex = 1
                }
                
                
                
            } else {
                print("Document does not exist")
            }
        }
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //Name
        userEmail.text = Auth.auth().currentUser?.email!
        userName.text = Auth.auth().currentUser?.displayName
        
        //Image
        userImage.layer.cornerRadius = self.userImage.frame.size.width / 2
        userImage.clipsToBounds = true
        let url = Auth.auth().currentUser?.photoURL
        let data = try? Data(contentsOf: url!) //make sure your image in this url does exist, otherwise unwrap in a if let check / try-catch
        userImage.image = UIImage(data: data!)
       
    }
    
    @IBAction func SaveBtn(_ sender: UIButton) {
        
        let db = Firestore.firestore()

        var fam = true
        if (userFamily.selectedSegmentIndex == 0){
            fam = true
        }
        else{
            fam = false
        }
        
        var sex = true
        if (userSex.selectedSegmentIndex == 0){
            sex = true
        }
        else{
            sex = false
        }
        
        var smoke = true
        if (userSmoker.selectedSegmentIndex == 0){
            smoke = true
        }
        else{
            smoke = false
        }
        
        db.collection("profile").document("users").setData([
            "age": userAge.text,
            "chol": userChol.text,
            "family-history": fam ,
            "height": userSize.text,
            "phone": userPhone.text,
            "sex": sex,
            "smoking-5": smoke,
            "weight": userWeight.text
        ], merge: true ) { err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
            }
        }
        
    }
    

}
