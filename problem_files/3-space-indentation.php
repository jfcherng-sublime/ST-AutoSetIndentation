<!-- https://forum.sublimetext.com/t/detect-indentation-with-3-spaces-is-broken/45143 -->
<!-- Guess settings from buffer: Detected as Space/2 but should be Space/3 -->
<?php

class Test extends TestAbstract implements TestInterface {

   /**
    * Lorem ipsum dolor sit amet
    * Lorem ipsum dolor sit amet
    *
    * @param string $test
    * @param array $testArray
    */
   public function __construct (string $test, array $testArray) {
      if ($test == $testArray) {
         return false;
      } else {
         return true;
      }
   }

}
