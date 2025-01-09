package tf.irisc.chal.webwebhookhook

import java.net.URI
import java.net.URL

class StateType(
        hook: String,
        var template: String,
        var response: String
        ) {
    var hook: URL = URI.create(hook).toURL()
}

object State {
    var arr = ArrayList<StateType>()
}