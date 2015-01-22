package com.ntsdev.api;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ApiController {

    @RequestMapping("/board")
    public String gameBoard() {
        return "Here's the game board!";
    }
}
