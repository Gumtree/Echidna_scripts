<workflow>
  <task classname="au.gov.ansto.bragg.echidna.exp.task.HeaderInformationBlockTask">
    <parameters/>
    <dataModel class="org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock">
      <commands>
        <org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
          <sicsVariable>drive sc</sicsVariable>
          <value>0</value>
          <isQuoted>false</isQuoted>
        </org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
        <org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
          <sicsVariable>title</sicsVariable>
          <isQuoted>true</isQuoted>
        </org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
        <org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
          <sicsVariable>sampledescription</sicsVariable>
          <isQuoted>true</isQuoted>
        </org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
        <org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
          <sicsVariable>user</sicsVariable>
          <isQuoted>true</isQuoted>
        </org.gumtree.gumnix.sics.batch.ui.commands.SicsVariableCommand>
      </commands>
    </dataModel>
  </task>
  <task classname="au.gov.ansto.bragg.echidna.exp.task.SicsScriptBlockTask">
    <parameters/>
    <dataModel class="org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock">
      <commands>
        <org.gumtree.gumnix.sics.batch.ui.commands.ScriptCommand>
          <text></text>
        </org.gumtree.gumnix.sics.batch.ui.commands.ScriptCommand>
      </commands>
    </dataModel>
  </task>
  <task classname="au.gov.ansto.bragg.echidna.exp.task.DoRTScanTask">
    <parameters/>
    <dataModel class="org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock">
      <commands>
        <au.gov.ansto.bragg.echidna.exp.command.DoRTCommand>
          <overlaps>1</overlaps>
          <stepsize>0.05</stepsize>
          <size>9</size>
          <sampposAB>A</sampposAB>
          <sampposNumber>1</sampposNumber>
          <tot__time>1.0</tot__time>
        </au.gov.ansto.bragg.echidna.exp.command.DoRTCommand>
      </commands>
    </dataModel>
  </task>
  <context>
    <org.gumtree.gumnix.sics.batch.ui.model.SicsBatchScript>
      <org.gumtree.gumnix.sics.batch.ui.model.SicsBatchScript>
        <blocks>
          <org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock reference="../../../../../task/dataModel"/>
          <org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock reference="../../../../../task[2]/dataModel"/>
          <org.gumtree.gumnix.sics.batch.ui.model.SicsCommandBlock reference="../../../../../task[3]/dataModel"/>
        </blocks>
      </org.gumtree.gumnix.sics.batch.ui.model.SicsBatchScript>
    </org.gumtree.gumnix.sics.batch.ui.model.SicsBatchScript>
  </context>
  <parameters/>
</workflow>