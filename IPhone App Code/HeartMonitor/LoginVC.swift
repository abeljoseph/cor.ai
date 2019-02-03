//
//  LoginVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import Firebase
import GoogleSignIn

class LoginVC: UIViewController, GIDSignInUIDelegate {
    
    override func viewDidAppear(_ animated: Bool) {
    
        super.viewDidAppear(animated)
        
        GIDSignIn.sharedInstance().uiDelegate = self
        GIDSignIn.sharedInstance().signIn()
        
    }

    func sign(inWillDispatch signIn: GIDSignIn!, error: Error!) {
        performSegue(withIdentifier: "ToApp", sender: self)
    }
    
    func sign(_ signIn: GIDSignIn!, dismiss viewController: UIViewController!) {
        //
    }
    
    func sign(_ signIn: GIDSignIn!, present viewController: UIViewController!) {
        //
    }
    
}
