package tf.irisc.chal.webwebhookhook

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class WebwebhookhookApplication

const val FLAG = "irisctf{url_equals_rebind}";

fun main(args: Array<String>) {
    State.arr.add(StateType(
            "http://example.com/admin",
            "{\"data\": _DATA_, \"flag\": \"" + FLAG + "\"}",
            "{\"response\": \"ok\"}"))
    runApplication<WebwebhookhookApplication>(*args)
}
