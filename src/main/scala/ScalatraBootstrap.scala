import com.rts.tictactoe.services._
import org.scalatra._
import javax.servlet.ServletContext

class ScalatraBootstrap extends LifeCycle {
  override def init(context: ServletContext) {
    context.mount(new ComputerPlayer, "/computerPlayer");
    context.mount(new Winner, "/winner")

  }
}
