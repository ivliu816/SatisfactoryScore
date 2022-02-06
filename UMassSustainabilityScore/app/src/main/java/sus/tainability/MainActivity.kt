package sus.tainability

import android.R.*
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity(){
    private var progr = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        val f = resources.getStringArray(R.array.foods)
        val l = resources.getStringArray(R.array.locations)
        val spinner: Spinner = findViewById(R.id.food_spinner)
        val spin : Spinner = findViewById(R.id.locate_spinner)
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, f)
        val adapt = ArrayAdapter(this, android.R.layout.simple_spinner_item, l)
        spinner.adapter = adapter
        spin.adapter = adapt
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapt.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        spinner.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View,
                position: Int,
                id: Long
            ) {
                Toast.makeText(this@MainActivity, f[position], Toast.LENGTH_SHORT).show()
                if(progr <= 95) {
                    progr += 5;
                    updateProgressBar()
                }
            }

            override fun onNothingSelected(parent: AdapterView<*>) {
                // write code to perform some action
            }
        }

        spin.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View,
                position: Int,
                id: Long
            ) {
                Toast.makeText(this@MainActivity, l[position], Toast.LENGTH_SHORT).show()
                progr += 5
            }

            override fun onNothingSelected(parent: AdapterView<*>) {
                // write code to perform some action
            }
        }
    }

    private fun updateProgressBar() {
        progress_bar.progress = progr
        text_view_progress.text = "$progr"
    }

}