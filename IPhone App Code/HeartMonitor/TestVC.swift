//
//  TestVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit

class TestVC: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func fitbit(_ sender: UIButton) {
        
        performSegue(withIdentifier: "fitbit", sender: self)

    }
    
    
    @IBAction func manual(_ sender: UIButton) {
        
        performSegue(withIdentifier: "manual", sender: self)

    }
    
}
