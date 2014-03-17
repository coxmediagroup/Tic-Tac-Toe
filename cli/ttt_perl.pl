#!/usr/bin/perl

use Data::Dumper;

my $gridSize = 3;
my @grid;

my @lines = (
                [ 0, 1, 2 ],
                [ 3, 4, 5 ],
                [ 6, 7, 8 ],
                [ 0, 3, 6 ],
                [ 1, 4, 7 ],
                [ 2, 5, 8 ],
                [ 0, 4, 8 ],
                [ 2, 4, 6 ]
            );

my @bestLocs = qw(4 8 6 2 0 7 5 3 1);

init();

printBoard();

while(1){
    print "Place your 'X': ";
    chomp(my $location = <STDIN>);
    $location =~ s/\D//g;
    if($location>0 and $location <10 and $grid[$location-1]){
        if($grid[$location-1]=~/\d/){
            $grid[$location-1] = 'X';
            if(!checkBoard()){
                getNextMove();
            }
        }else{
            print "Bad move.\n";
        }
        printBoard();
    }
    checkBoard();
}

sub init{
    my $count = 1;
    foreach my $loc (0..($gridSize*$gridSize)-1){
        $grid[$loc] = $count;
        $count++;
    }
}


sub printBoard{
    my $last = shift;
    print "+---+---+---+\n";
    foreach my $loc (0..($gridSize*$gridSize)-1){
        if($last){
            printf "|   " if $grid[$loc]=~/\d/;
            printf "| $grid[$loc] " if $grid[$loc]=~/\D/;
        }else{
            printf "| $grid[$loc] ";
        }
        print "|\n+---+---+---+\n" if ($loc+1) % $gridSize == 0;
    }
}

sub checkBoard{
    foreach my $line (@lines){
        my $sum = 0;
        my $openLoc = 0;
        foreach $loc (@$line){
            if($grid[$loc] eq 'X'){
                $sum += 1;
            }elsif($grid[$loc] eq 'O'){
                $sum += -1;
            }else{
                $openLoc = $loc;
            }
        }
        if($sum==3){
            print "X Wins!\n";
            printBoard("last");
            exit;
        }elsif($sum == -3){
            print "O Wins!\n";
            printBoard("last");
            exit;
        }
    }
    foreach my $loc (@grid){
        if($loc =~ /\d/){
            return 0;
        }
    }
    print "TIE!\n";
    printBoard("last");
    exit;
}

sub getNextMove{
    foreach my $line (@lines){
        my $sum = 0;
        my $openLoc = -1;
        foreach $loc (@$line){
            if($grid[$loc] eq 'X'){
                $sum += 1;
            }elsif($grid[$loc] eq 'O'){
                $sum += -1;
            }else{
                $openLoc = $loc;
            }
        }
        if($sum == -2 and $openLoc >= 0){
            $grid[$openLoc]='O';
            return 0;
        }
    }
    foreach my $line (@lines){
        my $sum = 0;
        my $openLoc = -1;
        foreach $loc (@$line){
            if($grid[$loc] eq 'X'){
                $sum += 1;
            }elsif($grid[$loc] eq 'O'){
                $sum += -1;
            }else{
                $openLoc = $loc;
            }
        }
        if($sum == 2 and $openLoc >= 0){
            $grid[$openLoc]='O';
            return 0;
        }
    }
    foreach my $line (($lines[6], $lines[7])){
        my $sum = 0;
        my $openLoc = -1;
        foreach $loc (@$line){
            if($grid[$loc] eq 'X'){
                $sum += 1;
            }elsif($grid[$loc] eq 'O'){
                $sum += -1;
            }else{
                $openLoc = $loc;
            }
        }
        if($sum == 0 and $openLoc >= 0){
            $grid[$openLoc]='O';
            return 0;
        }
    }
    foreach my $bestLoc (@bestLocs){
        if($grid[$bestLoc]=~/\d/){
            $grid[$bestLoc]='O';
            return 0;
        }
    }
}
