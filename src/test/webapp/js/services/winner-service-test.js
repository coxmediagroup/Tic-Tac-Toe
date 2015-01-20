WinnerServiceTest = TestCase("WinnerServiceTest");

WinnerServiceTest.prototype.convertCommaDelimitedStringToIntArray = function(){
	var winnerService = new WinnerService();
	assertEquals(Array(-1,-1,-1), winnerService.convertCommaDelimitedStringToIntArray("-1,-1,-1"));
};