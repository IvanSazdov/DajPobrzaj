using DajPobrzajApi.Dto;
using DajPobrzajApi.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Text.Json;

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
            var filePath = @"C:\Users\ivan.sazdov\Desktop\carsData.json";

            // Read existing data
            var existingData = System.IO.File.Exists(filePath)
                               ? System.IO.File.ReadAllText(filePath)
                               : "[]";

            var carsList = JsonSerializer.Deserialize<List<CarsDto>>(existingData);

            // Add new data
            carsList.Add(cars);

            // Write back to file
            System.IO.File.WriteAllText(filePath, JsonSerializer.Serialize(carsList));


            return Ok();
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("GetCarsData")]
        public IActionResult GetCarsData()
        {
            var filepath = @"C:\Users\ivan.sazdov\Desktop\carsData.json";
            var file = System.IO.File.OpenRead(filepath);

            var carsList = JsonSerializer.Deserialize<List<CarsDto>>(file);
            return new JsonResult(carsList);
        }
    }
}
