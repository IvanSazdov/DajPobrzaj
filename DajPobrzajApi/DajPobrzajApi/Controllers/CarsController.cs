using DajPobrzajApi.Dto;
using DajPobrzajApi.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace DajPobrzajApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CarsController : ControllerBase
    {
        
        [HttpPost]
        [AllowAnonymous]
        [Route("SendCarsData")]
        public IActionResult SendCarsData(CarsDto cars)
        {
            var result = cars;

            return Ok();
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("GetCarsData")]
        public IActionResult GetCarsData()
        {
            return Ok();
        }
    }
}
