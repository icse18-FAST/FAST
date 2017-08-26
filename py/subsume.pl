my $Mutant_matrix = "$ARGV[0]";

%kil_matrix = ( );
%kil_matrix2 = ( );
%killMatrixNew = ();
@mutants=();
%SelectedMutants = ();

readKillMatrixChris();
DetermineMinimum();


sub DetermineMinimum( ){
    my %SubsumedMutants = ();
    my %CurrliveMutants = map { $_ => 1 } @mutants;
    my %discardedMutants = ();
    
    foreach my $mut (keys %CurrliveMutants) {
        if ( @{$kil_matrix{$mut}} == 0 ){
            delete $CurrliveMutants{$mut};
        }
        else{
            my $size = 0;
            my $initialTest;
            foreach my $test (@{$kil_matrix{$mut}}) {
                if ( @{$kil_matrix2{$test}} > $size ){
                    $initialTest = $test;
                    $size = @{$kil_matrix2{$test}};
                }
            }
            @{$SubsumedMutants{$mut}} = @{$kil_matrix2{$initialTest}};
            foreach my $test (@{$kil_matrix{$mut}}) {
                my %CurrSubsumedMutants=map{$_ =>1} @{$SubsumedMutants{$mut}};
                @{$SubsumedMutants{$mut}} = grep( $CurrSubsumedMutants{$_}, @{$kil_matrix2{$test}} );
            }
        }
	}    

    while ( %CurrliveMutants ){
        my $size = 0;
        my $currMut;
        foreach my $mut (keys %CurrliveMutants) {
            if ( @{$SubsumedMutants{$mut}} > $size ){
                $currMut = $mut;
                $size = @{$SubsumedMutants{$mut}};
            }
        }
        $SelectedMutants{$currMut} = 1;
        $discardedMutants{$currMut} = 1;
        delete $CurrliveMutants{$currMut};
        foreach my $mut (@{$SubsumedMutants{$currMut}}) {
            $discardedMutants{$mut} = 1;
            delete $CurrliveMutants{$mut};
        }
        foreach my $mut (keys %SubsumedMutants ) {
            @{$SubsumedMutants{$mut}} = grep(!defined $discardedMutants{$_}, @{$SubsumedMutants{$mut}});
        }
    }
    foreach my $mut (keys %SelectedMutants) {
        print "$mut \n";
    }
}

sub readKillMatrixChris( ){
    open(INPUT, "<$Mutant_matrix") or die;
    $testid = 0;
    while(<INPUT>) {
        $line = trim($_);
        if ( length($line) == 0 ){
            next;
        }
        my @values = split(' ', $line);
        
        $testid = scalar $values[1];$testid--;
        push(@{$kil_matrix{$values[0]}}, $testid );
        push(@{$kil_matrix2{$testid}}, $values[0] );
        $killMatrixNew{$testid}{$values[0]}=1;
    }
    close(INPUT);
    foreach my $mutant (keys %kil_matrix){
        push @mutants, $mutant;
    }
}

sub trim($){
	my $string = shift();
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}
