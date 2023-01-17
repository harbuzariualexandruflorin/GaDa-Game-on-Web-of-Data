using Microsoft.AspNetCore.Http;
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

        [HttpGet("answer")]
        public IActionResult Answer(string question)
        {
            var query = quizService.GetQueryOfQuestion(question);

            var queryResult = quizService.GetQueryAnswer(query);

            return Ok(queryResult);
        }

        [HttpPost("getQuestion")]
        public IActionResult GetQuestion([FromBody] Data data)
        {
            //var question = quizService.GetRandomQuestion(topic);

            if (data.characters == null || data.characters.Count == 0)
            {
                return BadRequest();
            }

            var question = quizService.GetRandomQuestion(data.characters);

            return Ok(question);
        }
    }
}
