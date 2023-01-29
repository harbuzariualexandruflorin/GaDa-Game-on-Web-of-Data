using Microsoft.AspNetCore.Mvc;
using QuizAPI.Core;
using QuizAPI.Services;

namespace QuizAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class QuestionController : ControllerBase
    {
        private readonly IQuizService quizService;

        public QuestionController(IQuizService quizService)
        {
            this.quizService = quizService;
        }

        [HttpPost("answer")]
        public IActionResult CheckAnswer([FromBody] Answer answer)
        {

            var response = quizService.CheckAnswer(answer);

            return Ok(response);
        }

        [HttpPost("getQuestion")]
        [Produces("application/json")]
        public IActionResult GetQuestion([FromBody] Data data)
        {

            if (data.characters == null || data.characters.Count == 0 || data.characters.Contains(""))
            {
                return BadRequest();
            }

            var nrOfQuestions = (int)Math.Ceiling((float)data.characters.Count / 2);

            var question = quizService.GetQuestions(data.characters, nrOfQuestions);

            return Ok(question);
        }
    }
}
