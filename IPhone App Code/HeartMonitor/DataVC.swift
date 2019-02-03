//
//  DataVC.swift
//  HeartMonitor
//
//  Created by Sagar Patel on 2019-02-02.
//  Copyright © 2019 Sagar Patel. All rights reserved.
//

import UIKit
import Charts
import Firebase
import FirebaseFirestore

class DataVC: UIViewController {

    @IBOutlet weak var chtChart: LineChartView!
    @IBOutlet weak var chtBar: BarChartView!
    
     //This is where we are going to store all the numbers. This can be a set of numbers that come from a Realm database, Core data, External API's or where ever else

    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        let db = Firestore.firestore()
        
        let main = db.collection("profile").document("users").collection("coredata")
        main.order(by: "date", descending: true).limit(to: 4).getDocuments() { (querySnapshot, err) in
            
            var userChol = ""
            var excNumbers : [Double] = []
            var cholNumbers : [Double] = []
            var excBase : [Double] = [75, 75, 75, 75]
            var cholBase : [Double] = [200, 200, 200, 200]
            
            for document in querySnapshot!.documents {
                
                var x = document.get("excmin") as! String
                var y:Double! = Double(x)
                
                excNumbers.append(y)
                
                var z = document.get("chol") as! String
                var zz:Double! = Double(x)
                
                cholNumbers.append(zz)
                
            }
           
            
            var lineChartEntry  = [ChartDataEntry]()
            var lineChartBase  = [ChartDataEntry]()
        
            for i in 0..<excNumbers.count {
                let value = ChartDataEntry(x: Double(i), y: excNumbers[i])
                lineChartEntry.append(value)
            }
            
            for i in 0..<excBase.count {
                let value = ChartDataEntry(x: Double(i), y: excBase[i])
                lineChartBase.append(value)
            }
            
            let line1 = LineChartDataSet(values: lineChartEntry, label: "Your Data")
            line1.colors = [NSUIColor.blue]
            let line2 = LineChartDataSet(values: lineChartBase, label: "Healthy Avg.")
            line1.colors = [NSUIColor.blue]
            line2.colors = [NSUIColor.red]
            
            let data = LineChartData()

            data.addDataSet(line1)
            data.addDataSet(line2)
            
            self.chtChart.data = data
            self.chtChart.chartDescription?.text = "Excercise Minutes / Week"
            
            
            //G
            
            let entry1 = BarChartDataEntry(x: 1.0, y: Double(cholNumbers[0]))
            let entry2 = BarChartDataEntry(x: 2.0, y: Double(cholNumbers[1]))
            let entry3 = BarChartDataEntry(x: 3.0, y: Double(cholNumbers[2]))
            let entry4 = BarChartDataEntry(x: 4.0, y: Double(cholNumbers[3]))
            
            let dataSet = BarChartDataSet(values: [entry1, entry2, entry3, entry4], label: "Your Data")
            let bardata = BarChartData(dataSets: [dataSet])
            self.chtBar.data = bardata
            self.chtBar.chartDescription?.text = ""
            
            //All other additions to this function will go here
            
            //This must stay at end of function
            self.chtChart.notifyDataSetChanged()
            self.chtBar.chartDescription?.text = "Cholestrol"
            
            //All other additions to this function will go here
            
            //This must stay at end of function
            self.chtBar.notifyDataSetChanged()
            
        }
        
        
    }
 

}
