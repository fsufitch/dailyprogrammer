<?php
$MONEY = 500;
$solutions = array( 0 => array("sum" => 0, "choices" => array()) );
$solctr = 1;

function nextFruit() {
  if (($line = readline()) === false) return;
  $tokens = explode(' ',trim($line));
  $name = $tokens[0];
  $price = intval($tokens[1]);

  foreach ($GLOBALS["solutions"] as $solution) {
    for ($i = (int)(($GLOBALS["MONEY"]-$solution["sum"])/$price); $i>=1; $i--) {
      $newSolution = array( "sum" => $solution["sum"] + $price * $i,
			    "choices" => array_merge($solution["choices"],
						     array($i . " " . $name . ($i>1 ? "s" : ""))));
      if ($newSolution["sum"] <= $GLOBALS["MONEY"]) $GLOBALS["solutions"][$GLOBALS["solctr"]++] = $newSolution;
    }
  }

  foreach ($GLOBALS["solutions"] as $i => $solution) {
    if ($solution["sum"] == $GLOBALS["MONEY"]) echo implode(", ", $solution["choices"]) . "\n";
    if ($solution["sum"] >= $GLOBALS["MONEY"]) unset($GLOBALS["solutions"][$i]);
  }
  echo count($GLOBALS["solutions"]) . "\n";
  nextFruit();
}
nextFruit();